import numpy as np
from pathlib import Path
import pickle
import warnings
warnings.filterwarnings('ignore')

class PredictOnAPI():

    base_dir = Path(__file__).resolve().parent

    def __init__(self):
        pass

    # クラスメソッドのこと
    # @classmethodをクラス関数につけるだけ
    # 習慣で第一引数をselfではなく、clsと書く
    # 関数内ではインスタンs変数にはアクセスできないが、クラス変数にはアクセスできる
    # 他のクラスメソッドやスタティックメソッドにもアクセス可能
    # 要は、インスタンス変数に用事がない場合に使用できる
    @classmethod
    def __load_model(cls):
        '''
        pickle 形式で作成されたモデルを読み込む
        存在しない場合は作成する
        '''

        path_to_model = cls.base_dir / 'model' / 'model.pkl'
        with open(path_to_model, "rb") as f:
            model = pickle.load(f)

        return model

    # スタティックメソッド
    # インスタンスメソッドやクラスメソッドと異なり、指定される第一引数ではなく、
    # 必要な引数を1番目から書く
    # 関数内ではインスタンス変数や、クラス変数、他の関数にもアクセスできない
    # クラスの他の実装に依存しない関数
    # 要は、独立した関数として実装できる
    @staticmethod
    def encode_sex(x: str):
        if x == '男性':
            return 1
        elif x == '女性':
            return 0
        else:
            return np.nan

    @staticmethod
    def __encode_pclass(x: str):
        if x == '上層クラス (資産階級)':
            return 1
        elif x == '中層クラス (一般階級)':
            return 2
        elif x == '下層クラス (労働階級)':
            return 3
        else:
            return np.nan

    @staticmethod
    def count_family_feature(parch: int, sibsp: int):
        # 最後の1は本人のこと
        return parch + sibsp + 1

    @staticmethod
    def mean_Fare_by_Sex(x: str):
        if x == '男性':
            return 26
        elif x == '女性':
            return 46
        else:
            return np.nan

    @classmethod
    def derive_survival_probability(
        cls,
        Pclass: str,
        Sex: str,
        Age: int,
        SibSp: int,
        Parch: int,
        Fare: int,
    ) -> float:
        '''
        与えられた特徴量について、
        事前に学習済みのモデルを用いてタイタニック生存確率を算出する
        '''
        model = cls.__load_model()

        encoded_sex = cls.encode_sex(Sex)
        encoded_pclass = cls.__encode_pclass(Pclass)
        Family = cls.count_family_feature(Parch, SibSp)
        mean_fare_by_sex = cls.mean_Fare_by_Sex(Sex)

        features = np.array([[
            encoded_pclass,
            encoded_sex,
            Age,
            SibSp,
            Parch,
            Fare,
            Family,
            mean_fare_by_sex,
        ]])

        survival_probability = model.predict(features)

        return float(np.round(survival_probability, 3)[0])


# 余談
# クラスやスタティックメソッドでなく全部インスタンスメソッドでいいのでは?
# インスタンスメソッドの例
# class MyClass:
#     CLASS_PARAM = 100

#     def __init__(self, instance_param):
#         self.instance_param = instance_param

#     def method(self):
#         print(self.CLASS_PARAM)

#     def method_2(self, param):
#         print("Static!!", param)

# 使い分けるメリット
# 1. 可読性/保守性: 別の関数で操作されたインスタンス変数がさらに別の関数で登場するケース
# - 一直線にコードが読めないのと、インスタンス変数への意識に脳のリソースが割かれ疲れる
# - 全部インスタンスメソッドにするとこの関数はどこかでインスタンス変数を操作しているのか??という
# - 割と重要な情報が、関数を全部読むまでわからない
# - 関数の頭にデコレータで@staticmethodとかけば「この関数はインスタンス変数にはアクセスしない」とわかる

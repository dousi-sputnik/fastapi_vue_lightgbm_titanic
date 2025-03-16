from fastapi import FastAPI
from pydantic import BaseModel
from machine_learning.titanic import PredictOnAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# デフォでは4000にあるフロントエンドと違う場所(オリジン)にある5000に存在するバックエンド間での通信は禁止されている
# そのため、限定的に異なるオリジン間で情報共有を許可するCORS(Cross Origin Resource Sharing)の設定を変更し
# 許可オリジンにフロントエンドを追加する必要がある
# allow_origins = の部分
app.add_middleware(
    CORSMiddleware,
    allow_origins = ['http://localhost:4000'],
    allow_methods = ['*'],
    allow_headers = ['*']
)

# @app.getでHTTPメソッドのうち、GETメソッドが使われることを指定
# 引数は窓口を設置する場所(エンドポイント)を指定
# @app.get('/helloworld')
# def get_hello_message():
#     return {"message": "Hello World"}

# GETメソッドを用いてフロントエンドからパラメータを渡すアプローチ
# パラメータとしてエンドポイントに渡したい変数は、{}で囲む。その変数名を内部に宣言する
# @app.get('/api/{message}')
# def get_any_message(message: str):
#     return {"message": message}

# POSTメソッドを用いたアプローチ
# POSTメソッドではリクエストボディというものにパラメータの情報を付加してバックエンドに渡す

# POSTメソッドで送られるパラメータの型を定義
# pydanticモジュール内のBaseModelクラスを定義し、その中でクラス変数を型付きで定義
# POSTメソッドでリクエストボディとしてフロントエンドからバックエンドに渡されるパラメータを定義
class SchemaOfTitanicFeaturesRequest(BaseModel):
    Pclass: str
    Sex: str
    Age: int
    SibSp: int
    Parch: int
    Fare: int

class SchemaOfSurvivalProbabilityResponse(BaseModel):
    survival_probability: float

# response_modelという引数に、バックエンドからフロントエンドに返却されるデータの型を定義したクラス
# (直前で作成したSchemaOfTitanicFeaturesRequest のこと)
# SchemaOfTitanicFeaturesRequestは「フロントからバックに渡すパラメータの型を定義したもの」であって
# 「バックエンドからフロントエンドに返すパラメータの型を定義したもの」ではない
# 今回は「フロントから受け取ったパラメータをそのままバックエンドから返却するAPI」のため問題ない
# @app.post('/api/titanic', response_model=SchemaOfTitanicFeaturesRequest)
# def derive_score(request_body: SchemaOfTitanicFeaturesRequest):
#     return request_body

# response_modelをSchemaOfSurvivalProbabilityResponseに変更した。元々は与えられたパラメータをそのまま返すAPI
# 今夏は与えられたパラメータを元に確率値を返すAPIに変更したため
@app.post('/api/titanic', response_model=SchemaOfSurvivalProbabilityResponse)
def derive_score(request_body: SchemaOfTitanicFeaturesRequest):
    # 辞書オブジェクトに変更
    # 目的は、PredictOnAPI.derive_survival_probabilityの引数として渡したいため。
    # 辞書型の理由としては1. キーワード引数との対応 2. 柔軟性にある
    # 1. Pythonの関数はキーワード引数をkey=valueの形で引数を渡せれる
    # - 辞書型のkeyはキーワード引数のkeyに、valueはキーワード引数のvalueに対応する
    # - よって、**演算子を使い辞書を展開すると、キーワード引数として関数に渡される
    # 2. 辞書型は、キーと値のペアを格納できるので、引数の数が可変の場合や、引数の順序が不定の場合に便利
    features_dict = request_body.__dict__
    # **<辞書オブジェクト>とすることで、引数として自動的にバラして与えることが可能
    survival_probability = PredictOnAPI.derive_survival_probability(**features_dict)
    return {'survival_probability': survival_probability}

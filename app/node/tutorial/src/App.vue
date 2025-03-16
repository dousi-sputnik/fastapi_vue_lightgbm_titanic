<script setup lang="ts">
import { ref, reactive, computed } from "vue";
import axios from "axios";

// 型を定義する場合は冒頭に type を使用する
type typeOfFeatures = {
  Pclass: string;
  Sex: "男性" | "女性" | "性別";
  Age: number | "年齢";
  SibSp: number | "兄弟姉妹の同伴数";
  Parch: number | "親・子の同伴数";
  Fare: number | "運賃($)";
};

// reactiveはオブジェクト(変数)を保存できる箱
// 変数の箱を定義し、それらの初期値を定めている。
// const 変数名<型情報>({初期値の情報})
// v-modelは双方向バインディングで、html上のデータと別のデータを連携させる機能を持つ。
// 今回はhtml上でユーザーが選択するセレクタの情報と、その情報の保存先として作成した箱(features)
// の情報を連動させるように設定する。
const features = reactive<typeOfFeatures>({
  Pclass: "階級",
  Sex: "性別",
  Age: "年齢",
  SibSp: "兄弟姉妹の同伴数",
  Parch: "親・子の同伴数",
  Fare: "運賃($)",
});

// typescriptではアロー関数を定義する場合は以下の記法で定義を行う
// const functionName = (x: type1): type2 => {...}
// x: type1の部分は、引数とその型で、複数あればカンマで区切って追加する
// type2は返り値の型で、返り値が存在しない場合はvoidと記述します。
// ``の部分はテンプレートリテラルという箇所で、開業したり、${}の中括弧内に変数を書き込むことで、変数を代入したものを文字列とできる
// const displayOutput = (): void => {
//   alert(
//     `
//     性別: ${features.Sex}
//     階級: ${features.Pclass}
//     年齢: ${features.Age}
//     運賃: ${features.Fare}
//     親・子の同伴数: ${features.Parch}
//     兄弟姉妹の同伴数: ${features.SibSp}
//     `
//   );
// };

const selectFare = computed(() => {
  const startFare = 5;
  const endFare = 500;
  const resultFare = [];
  for (let i = startFare; i <= endFare; i += 5) {
    resultFare.push(i);
  }
  return resultFare;
});

// 生存確率を格納するための変数を定義
// ref は単一の変数を格納するための変数を作成するときに使用
// const 変数名 = ref<変数の型>(初期値)
// 初期値は何も書かないと自動的に undefined と認識される
// 今回は初期値を設定しないので、型情報のところで number|undefinedと記述し、undefinedの可能性を宣言した
const survivalProbability = ref<number | undefined>();

// バリデーションのための関数を定義
// TypeScriptの関数(アロー関数)の定義方法は下記
// const 関数名 = (引数1: 引数1の型,...): 返り値の型 => {関数処理}
const validateRequestValues = (): boolean => {
  if (features.Pclass == "階級") {
    alert("階級を選択してください");
    return false;
  }
  if (features.Sex == "性別") {
    alert("性別を選択してください");
    return false;
  }
  if (features.Age == "年齢") {
    alert("年齢を選択してください");
    return false;
  }
  if (features.SibSp == "兄弟姉妹の同伴数") {
    alert("兄弟姉妹の同伴数を選択してください");
    return false;
  }
  if (features.Parch == "親・子の同伴数") {
    alert("親・子の同伴数を選択してください");
    return false;
  }
  if (features.Fare == "運賃($)") {
    alert("運賃を選択してください");
    return false;
  }
  // 全ての条件に引っ掛からなかった場合にのみ true を返す
  return true;
};

const displayOutput = (): void => {
  // エンドポイントを指定
  const endPoint: string = "http://localhost:8080/api/titanic";
  // バリデーションの実行
  const validationResult: boolean = validateRequestValues();
  // バリデーションに成功していれば axios を実行
  if (validationResult === true) {
    // axios.postで POST メソッドを実行することを指示
    // 第一引数にエンドポイント, 第二引数にリクエストボディを指定
    axios
      .post(endPoint, features)
      .then(
        // then 以下で問題なくレスポンスが帰ってきた際の挙動を記述
        (response) => {
          // TypeScriptの型指定は後ろに as をこのようにつけることでも指定可能
          // refを用いて定義した場合、script内で値にアクセスするためには.valueをつける
          // しかしtemplate内では.valueをつけない点に注意
          // reactiveモジュールの場合はどちらの場合にも.valueをつけないでアクセスできる
          survivalProbability.value = (100 *
            response.data.survival_probability) as number;
        }
      )
      .catch(
        // catch 以下でエラーが発生した場合の挙動を記述
        (error) => {
          alert(error);
        }
      );
  }
};
</script>

<template>
  <div class="navbar bg-blue-400 shadow-sw">
    <div class="flex flex-col">
      <span class="text-xl font-bold"
        >タイタニック号: AIは見た! あなたの生存確率</span
      >
      <span class="text-sm">-VueとFastAPIによる機械学習アプリ-</span>
    </div>
  </div>
  <!-- containerとmx-autoは「左右の余白をいい感じに調整してください」と指示している
  セットで覚える -->
  <div class="container mx-auto mt-4">
    <label class="label">階級</label>
    <br />
    <select class="select select-primary mb-1" v-model="features.Pclass">
      <option disabled selected>階級</option>
      <option>上層クラス (資産階級)</option>
      <option>中層クラス (一般階級)</option>
      <option>下層クラス (労働階級)</option>
    </select>
    <br />
    <label class="label">性別</label>
    <br />
    <select class="select select-primary mb-1" v-model="features.Sex">
      <option disabled selected>性別</option>
      <option>男性</option>
      <option>女性</option>
    </select>
    <br />
    <label class="label">年齢</label>
    <br />
    <select class="select select-primary mb-1" v-model="features.Age">
      <option disabled selected>年齢</option>
      <!-- ...はスプレッド構文を使用して、イテレータによって生成された値を新しい配列に展開する。
      結果として、0-120までの数値を含む配列を作成される。
      Array(121).keys(): 配列のindexを反復処理するためのイテレータを返す。 -->
      <option v-for="i in [...Array(121).keys()]">
        {{ i }}
      </option>
    </select>
    <br />
    <label class="label">兄弟姉妹の同伴数</label>
    <br />
    <select class="select select-primary mb-1" v-model="features.SibSp">
      <option disabled selected>兄弟姉妹の同伴数</option>
      <option v-for="i in [...Array(11).keys()]">
        {{ i }}
      </option>
    </select>
    <br />
    <label class="label">親・子の同伴数</label>
    <br />
    <select class="select select-primary mb-1" v-model="features.Parch">
      <option disabled selected>親・子の同伴数</option>
      <option v-for="i in [...Array(11).keys()]">
        {{ i }}
      </option>
    </select>
    <br />
    <label class="label">運賃($)</label>
    <br />
    <select class="select select-primary mb-4" v-model="features.Fare">
      <option disabled selected>運賃($)</option>
      <option v-for="i in selectFare">
        {{ i }}
      </option>
    </select>
    <br />
    <button class="btn btn-primary mb-2" @click="displayOutput()">
      生存率推定
    </button>
    <!-- <template></template>は<div></div>と異なり、まとまりを作るだけで、最終的なソースコードからはタグが消失する特徴がある -->
    <template v-if="survivalProbability !== undefined">
      <div class="alert alert-error">
        あなたの生存確率は {{ Math.round(survivalProbability) }} % です。
      </div>
    </template>
  </div>
</template>

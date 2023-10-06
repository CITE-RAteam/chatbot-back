# TUT Chatbot

## dynamodbにデータを新規登録する際の形式

dynamodbに登録する際は以下のjson形式を使用して下さい

```json
{
  "question_id": 1000, # int形式
  "next_choices": [ # 必須項目では無いので、あってもなくても構いません。
    {
      "choice_id": 2000,
      "choice_text": "hogeの方法" # 提示する選択肢のテキスト
    },
    {
      "choice_id": 2001,
      "choice_text": "barの方法"
    }
  ],
  "free_response": "fugaの方法はこちらです。" # 問題の解決方法や、選択肢の説明
}
```

## setup aws-cli

1. aws-cliをインストールする
1. `aws configure`を実行しておく
1. AWSアカウントを発行する
1. AWSアクセスキーをIAMコンソールから発行する
1. 発行した情報を、`aws configure`にコピペする
    - この順番をとることで、セキュリティリスクとなるクレデンシャル情報の流出を極限まで抑えることができる

**注意点**  
複数のIAMユーザーを使い分けるには、プロファイルを設定する必要が有ります。  
ここではその方法について触れないので、必要な場合は自力で調べて下さい。

## setup github actions

1. S3にデプロイ用のバケットを作成する。
1. [github actionsの為のIDプロバイダを設定する](https://docs.github.com/ja/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services)
1. IDプロバイダ用にPolicyを作成する。(作成例は下記の通り)
1. Secretを必要な分だけ記述する
   - `AWS_S3_BUCKET`: 先程作成したバケット名をいれる
   - `AWS_ACCOUNT_ID`: AWSのデプロイ用アカウントID
   - `AWS_GITHUB_OIDC_ROLE_NAME`: 作成したロール名
   - `OPENAI_API_KEY`: OpenAIのAPIキー。現時点では機能が未実装

### IDプロバイダに付与するPolicyの一例

ここでは多くの権限が付与されていますが、本来は必要最低限の権限を付与するよう、注意が必要です。

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "VisualEditor0",
      "Effect": "Allow",
      "Action": [
        "dynamodb:*",
        "cloudformation:*",
        "s3:*",
        "lambda:*",
        "apigateway:*",
        "iam:CreateRole",
        "iam:DeleteRole",
        "iam:GetRole",
        "iam:PassRole",
        "iam:DeleteRolePolicy",
        "iam:GetRolePolicy",
        "iam:AttachRolePolicy",
        "iam:DetachRolePolicy",
        "iam:PutRolePolicy",
        "iam:TagRole"
      ],
      "Resource": "*"
    }
  ]
}
```

## Local Debug 方法

### set environment

`.open_ai_api_key`ファイルを作成し、OpenAIのAPIキーを追加  
`.pr_num`ファイルを作成し、任意のPR番号か`main`と記載する

### local 実行

```sh
sam build && sam local start-api --parameter-overrides PrNumber=$(cat .pr_num) OpenAiApiKey=$(cat .open_ai_api_key)
```

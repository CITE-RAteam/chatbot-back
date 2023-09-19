# TUT Chatbot

## setup aws-cli

1. AWSアカウントを発行する
1. AWSアクセスキーをIAMコンソールから発行する
1. aws-cliをインストールする
1. `aws configure`を実行し、先程発行したアクセスキーを登録する

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

ここでは、多くの権限が付与されていますが、本来は必要最低限の権限を付与するよう、注意が必要です。

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
`.pr_num`ファイルを作成し、任意のPR番号か`dev`と記載する

### local 実行

```sh
sam build && sam local start-api --parameter-overrides PrNumber=$(cat .pr_num) OpenAiApiKey=$(cat .open_ai_api_key)
```

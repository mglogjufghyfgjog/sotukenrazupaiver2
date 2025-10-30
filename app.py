# --- app.py ---

# 1. 必要なライブラリをインポートします
from flask import Flask, render_template, request, redirect, url_for, session, flash
import os  # セッションの暗号化キーを安全に生成するために使用します

# 2. Flaskアプリケーションのインスタンスを作成（初期化）します
# __name__ は、このファイルが直接実行されたことを示すPythonの特別な変数です
app = Flask(__name__)

# 3. セッション管理とflashメッセージのための「秘密鍵(Secret Key)」を設定します
# セッションデータ（例：ログイン状態）を改ざんから守るために暗号化します
# os.urandom(24)で推測困難なランダムな文字列を生成しています
app.config['SECRET_KEY'] = os.urandom(24)


# --- ルーティングの定義 ---

# 4. ルートURL ('/') にアクセスがあった場合の処理を定義します
@app.route('/')
def index():
    # 'index.html' テンプレートを描画（レンダリング）してユーザーに返します
    # HTML側では session.logged_in の有無で表示する初期画面を切り替えます
    return render_template('index.html')


# 5. '/login' URLへのアクセス処理を定義します
# methods=['GET', 'POST'] は、このURLがページの表示(GET)とフォームの送信(POST)の両方に対応することを示します
@app.route('/login', methods=['GET', 'POST'])
def login():
    # 6. もしリクエストが 'POST' (フォームからデータが送信された) 場合
    if request.method == 'POST':
        # 7. フォームから送信された 'user_id' と 'password' を取得します
        user_id = request.form['user_id']
        password = request.form['password']

        # 8. --- 本来はここでデータベースと照合します ---
        # ここでは、ダミーの認証ロジックを使用します
        # 職員IDが 'admin' かつ パスワードが 'pass123' の場合のみ認証成功とします
        if user_id == 'admin' and password == 'pass123':

            # 9. 認証成功：セッションに 'logged_in' として True (ログイン済み) を記録します
            session['logged_in'] = True
            # 10. セッションに 'user_id' を記録します (HTML側で「ようこそ admin さん」のように使えます)
            session['user_id'] = user_id

            # 11. 認証後のホームページ（ルートURL）にリダイレクト（転送）します
            return redirect(url_for('index'))
        else:
            # 12. 認証失敗：'flash' を使ってユーザーに表示するエラーメッセージを設定します
            flash('職員IDまたはパスワードが間違っています。')

            # 13. ログインページ（ルートURL）にリダイレクトします (HTML側でflashメッセージが表示されます)
            return redirect(url_for('index'))

    # 14. もしリクエストが 'GET' (単に /login ページにアクセスした) 場合
    # (現状の設計では / からログイン画面を表示するため、通常ここは通りませんが念のため)
    return redirect(url_for('index'))


# 15. '/logout' URLへのアクセス処理を定義します
@app.route('/logout')
def logout():
    # 16. セッションから 'logged_in' の情報を削除します
    session.pop('logged_in', None)
    # 17. セッションから 'user_id' の情報を削除します
    session.pop('user_id', None)

    # 18. ログアウト後にログインページ（ルートURL）にリダイレクトします
    return redirect(url_for('index'))


# 19. このスクリプトが直接実行された場合にのみ、開発用サーバーを起動します
if __name__ == '__main__':
    # debug=True にすると、コード変更時に自動でサーバーが再起動し、エラー表示が詳細になります (本番環境では False にします)
    app.run(debug=True)
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8" />
    <title>ログイン画面</title>
</head>
<body>
    <form action="login.php" method="GET">
      <label for="username">ユーザー名</label>
      <input type="text" name="username" /><br />
      <label for="password"> パスワード</label>
      <input type="password" name="password" /><br />
      <button for="submit">ログイン</button><br />
      <input type="reset" value="リセット" />
    </form>
    <?php
    $username = $_REQUEST["username"];
    $password = $_REQUEST["password"];

    if($username === "alice" && $password === "wonderland"){
        echo "こんにちは、aliceさん";
    } else{
        echo "ログインできませんでした";
    }
    ?>
</body>
</html>
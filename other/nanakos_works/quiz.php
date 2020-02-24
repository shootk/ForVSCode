<? php
$title = "関東の県はどれですか？";

$question = array();

$question = array("千葉県","東京都","宮城県","山形県");

$answer = $question[0];

shuffle($question);
?>

<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <title>クイズ</title>
  </head>

  <body>
    <h2><?php echo $title ?></h2>
    <form method="POST"  action="answer.php">
      <?php foreach($question as $value){ ?>
        <input type ="radio" name="question" value="<?php echo $value; ?>" /><?php echo $value; ?><br>
      <?php } ?>
      <input type ="hidden" name="answer" value="<?php echo $answer; ?>">
      <input type ="submit" value="回答する">
    </form>
  </body>
</html>
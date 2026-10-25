<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Download Files</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f9f9f9; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        h1 { color: #333; font-size: 24px; border-bottom: 2px solid #eee; padding-bottom: 10px; }
        ul { list-style-type: none; padding: 0; }
        li { margin: 12px 0; padding: 8px; background: #f0f4f8; border-radius: 4px; }
        a { text-decoration: none; color: #0066cc; font-weight: bold; display: block; }
        a:hover { color: #004499; }
    </style>
</head>
<body>

<div class="container">
    <h1>Available Downloads</h1>
    <ul>
        <?php
        // "." means scan the current directory where this file lives
        $dir = "."; 

        if (is_dir($dir)) {
            if ($dh = opendir($dir)) {
                while (($file = readdir($dh)) !== false) {
                    // Exclude hidden files, parent folder links, and this script itself
                    if ($file != "." && $file != ".." && $file != "index.php") {
                        echo "<li><a href='" . htmlspecialchars($file) . "' download>" . htmlspecialchars($file) . "</a></li>";
                    }
                }
                closedir($dh);
            }
        }
        ?>
    </ul>
</div>

</body>
</html>

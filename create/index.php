<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>HockeyConnect</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" type="text/css" href="../css/bootstrap.min.css">
        <link rel="stylesheet" type="text/css" href="../css/navbar-top-fixed.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    </head>
    <body>
        <nav class="navbar navbar-expand-md navbar-dark fixed-top bg-dark">
        <a class="navbar-brand" href="../"><img src="../img/logo_white.png" height="30px"></a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarCollapse">
            <ul class="navbar-nav mr-auto">
            <li class="nav-item">
                <a class="nav-link" href="../">Home</a>
            </li>
            <li class="nav-item active">
                <a class="nav-link" href="#">Create<span class="sr-only">(current)</span></a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="../review/">Review</a>
            </li>
            </ul>
        </div>
        </nav>

        <main role="main" class="container">
        <div class="jumbotron">
            <h1>Create a New Tryout</h1>
            <p class="lead">Be sure to adhere strictly to the templates provided otherwise issues may occur.<br>Delete the sample values from the templates before populating.</p>
            <a href="../res/newSamplePlayers.csv" download="Hockey_Connect_Players.csv" class="btn btn-lg btn-secondary fa fa-download"> Download Player List Template</a><br><br>
            <a href="../res/newSampleCriteria.csv" download="Hockey_Connect_Criteria.csv" class="btn btn-lg btn-secondary fa fa-download"> Download Evaluation Criteria Template</a><br><br><br><br>
            <h2>Upload Tryout Files:</h2><br>
            <form action="http://localhost:5000/createTryout" method="POST" enctype="multipart/form-data">
                <div class="form-group lead">
                    Players:<br>
                    <input type="file" name="csvfileplayers" accept=".csv"><br><br>
                </div>
                <div class="form-group lead">
                    Evaluation Criteria:<br>
                    <input type="file" name="csvfilecriteria" accept=".csv"><br><br>
                </div>
                <input type="submit" class="btn btn-primary" value="Create Tryout">
            </form>
        </div>
        </main>

        <script src="http://code.jquery.com/jquery.min.js"></script>
        <script src="../js/bootstrap.min.js"></script>
    </body>
</html>

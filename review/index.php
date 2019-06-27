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
            <li class="nav-item">
                <a class="nav-link" href="../create/">Create</a>
            </li>
            <li class="nav-item active">
                <a class="nav-link" href="#">Review<span class="sr-only">(current)</span></a>
            </li>
            </ul>
        </div>
        </nav>

        <main role="main" class="container">
        <div class="jumbotron">
            <h1>Review Tryout Records</h1>
            <p class="lead">To retrieve the records for your tryout, please input the tryout ID and then select whether you require the timed or skill evaluation records.</p>
            
            <form action="#" id="getfileform" method="GET" enctype="multipart/form-data">
            <div class="form-group lead">
                Tryout ID:<br>
                <input type="text" id="tryoutid"><br>
            </div>
            <button type="button" class="btn btn-lg btn-primary fa fa-download" onclick="getTimedEvals();">Timed Evaluations</button>
            <button type="button" class="btn btn-lg btn-primary fa fa-download" onclick="getSkillEvals();">Skill Evaluations</button>
            </form>
        </div>
        </main>

        <script src="http://code.jquery.com/jquery.min.js"></script>
        <script src="../js/bootstrap.min.js"></script>
        <script src="../js/getEvals.js"></script>
    </body>
</html>

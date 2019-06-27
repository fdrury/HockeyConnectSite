Create a New Tryout<br><br>
<form action="http://localhost:5000/createTryout" method="POST" enctype="multipart/form-data">
    Players: 
    <input type="file" name="csvfileplayers" accept=".csv"><br><br>
    Evaluation Criteria: 
    <input type="file" name="csvfilecriteria" accept=".csv"><br><br>
    <input type="submit" value="Create Tryout">
</form>
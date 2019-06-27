from flask import Flask, jsonify, request, send_file
from tempfile import NamedTemporaryFile
import pymssql
import datetime
import csv
import io

app = Flask(__name__)

sensitiveFile = open('sensitive.txt', 'r')
# endline character removed
server=sensitiveFile.readline()[:-1]
user=sensitiveFile.readline()[:-1]
password=sensitiveFile.readline()[:-1]
database=sensitiveFile.readline()[:-1]

@app.route('/player/<path:path>')
def player(path):
    with pymssql.connect(server, user, password, database) as conn:
        with conn.cursor(as_dict=True) as cursor:
            cursor.execute('SELECT FirstName, LastName, Number FROM Players WHERE ID = \'%s\';', path)
            row = cursor.fetchone()
            rows = []
            while row:
                rows.append(row)
                row = cursor.fetchone()
            return jsonify(rows)

@app.route('/tryout/<path:path>')
def tryout(path):
    with pymssql.connect(server, user, password, database) as conn:
        with conn.cursor(as_dict=True) as cursor:
            cursor.execute('SELECT Players.FirstName, Players.LastName, Players.ID FROM Players INNER JOIN PlayerTryouts ON Players.ID=PlayerTryouts.PlayerID AND PlayerTryouts.TryoutID = %s;', path)
            row = cursor.fetchone()
            rows = []
            while row:
                rows.append(row)
                row = cursor.fetchone()
            return jsonify(rows)

@app.route('/timedEval', methods = ['POST'])
def saveTimedEval():
    with pymssql.connect(server, user, password, database) as conn:
        with conn.cursor(as_dict=True) as cursor:
            print(request.is_json)
            content = request.get_json()
            print(content)
            playerID = int(content.get('playerID'))
            evaluator = content.get('evaluator')
            tryoutID = content.get('tryoutID')
            duration = content.get('duration')
            currentTime = datetime.datetime.now().strftime('%Y%m%d %H:%M:%S')
            cursor.execute('INSERT INTO TimedEvaluations(PlayerID, Evaluator, TryoutID, Duration, Date) VALUES (%d, %s, %d, %d, %s);', (playerID, evaluator, tryoutID, duration, currentTime))
            conn.commit()
            return jsonify({'Success' : 1})

@app.route('/getEvalCrit/<tryout>')
def getEvalCrit(tryout):
    with pymssql.connect(server, user, password, database) as conn:
        with conn.cursor(as_dict=True) as cursor:
            cursor.execute('SELECT Criteria.Name, Criteria.Description, Criteria.ID FROM Criteria INNER JOIN TryoutCriteria ON Criteria.ID=TryoutCriteria.CriteriaID AND TryoutCriteria.TryoutID = %s;', tryout)
            row = cursor.fetchone()
            rows = []
            while row:
                rows.append(row)
                row = cursor.fetchone()
            return jsonify(rows)

@app.route('/getGameEval/<tryout>/<evaluator>/<player>')
def loadGameEval(tryout, evaluator, player):
    with pymssql.connect(server, user, password, database) as conn:
        with conn.cursor(as_dict=True) as cursor:
            cursor.execute('SELECT a.* FROM SkillEvaluations a INNER JOIN (SELECT CriteriaID, MAX(Date) Date FROM SkillEvaluations GROUP BY CriteriaID) b ON a.CriteriaID = b.CriteriaID AND a.Date = b.Date WHERE a.TryoutID = %s AND a.Evaluator = %s AND a.PlayerID = %s;', (tryout, evaluator, player))
            return jsonify(cursor.fetchall())

@app.route('/getTimedEval/<tryout>/<evaluator>/<player>')
def loadTimedEval(tryout, evaluator, player):
    with pymssql.connect(server, user, password, database) as conn:
        with conn.cursor(as_dict=True) as cursor:
            cursor.execute('SELECT Duration FROM TimedEvaluations WHERE TryoutID = %s AND Evaluator = %s AND PlayerID = %s ORDER BY Date DESC;', (tryout, evaluator, player))
            return jsonify(cursor.fetchone())

@app.route('/postGameEval', methods = ['POST'])
def saveGameEval():
    with pymssql.connect(server, user, password, database) as conn:
        with conn.cursor(as_dict=True) as cursor:
            print(request.is_json)
            content = request.get_json()
            print(content)
            playerID = int(content.get('playerID'))
            tryoutID = content.get('tryoutID')
            evaluatorID = content.get('evaluatorID')
            currentTime = datetime.datetime.now().strftime('%Y%m%d %H:%M:%S')
            cursor.execute('SELECT CriteriaID FROM TryoutCriteria WHERE TryoutID = %s', (tryoutID))
            rows = cursor.fetchall()
            for row in rows:
                criteriaID = row.get('CriteriaID')
                value = content.get(str(criteriaID))
                cursor.execute('INSERT INTO SkillEvaluations(PlayerID, TryoutID, Evaluator, CriteriaID, Value, Date) VALUES (%d, %d, %d, %d, %d, %s);', (playerID, tryoutID, evaluatorID, criteriaID, value, currentTime))
            conn.commit()
            return jsonify({'Success' : 1})

@app.route('/createTryout', methods = ['POST'])
def createTryout():
    with pymssql.connect(server, user, password, database) as conn:
        with conn.cursor(as_dict=True) as cursor:
            if 'csvfileplayers' not in request.files or 'csvfilecriteria' not in request.files:
                print('No file found')
                return 'No file found'
            
            f_players = request.files['csvfileplayers']
            if not f_players:
                return 'No file'
            fileContentsPlayers = io.StringIO(f_players.stream.read().decode('utf-8'), newline=None)
            
            f_criteria = request.files['csvfilecriteria']
            if not f_criteria:
                return 'No file'
            fileContentsCriteria = io.StringIO(f_criteria.stream.read().decode('utf-8'), newline=None)
            
            cursor.execute('SELECT ID FROM Tryouts ORDER BY ID DESC')
            row = cursor.fetchone()
            newTryoutID = row.get('ID', 0) + 1
            cursor.execute('INSERT INTO Tryouts(ID) VALUES(%d);', newTryoutID)
            
            cursor.execute('SELECT ID FROM Players ORDER BY ID DESC')
            row = cursor.fetchone()
            nextPlayerID = row.get('ID', 0) + 1
            readerPlayers = csv.DictReader(fileContentsPlayers)
            for row in readerPlayers:
                rowID = row['ID']
                if rowID == '':
                    rowID = str(nextPlayerID)
                    nextPlayerID += 1
                cursor.execute('INSERT INTO Players(FirstName, LastName, ID) VALUES(%s, %s, %s);', (row['FirstName'], row['LastName'], rowID))
                cursor.execute('INSERT INTO PlayerTryouts(PlayerID, TryoutID) VALUES(%s, %d);', (rowID, newTryoutID))

            cursor.execute('SELECT ID FROM Criteria ORDER BY ID DESC')
            row = cursor.fetchone()
            nextCriteriaID = row.get('ID', 0) + 1
            readerCriteria = csv.DictReader(fileContentsCriteria)
            for row in readerCriteria:
                rowID = row['ID']
                if rowID == '':
                    rowID = str(nextCriteriaID)
                    nextCriteriaID += 1
                cursor.execute('INSERT INTO Criteria(ID, Name, Description) VALUES(%s, %s, %s);', (rowID, row['Name'], row['Description']))
                cursor.execute('INSERT INTO TryoutCriteria(TryoutID, CriteriaID) VALUES(%d, %s);', (newTryoutID, rowID))

            
            conn.commit()
            return ('File uploaded successfully. Your Tryout ID is %d' % newTryoutID)


@app.route('/downloadTimedEvals/<path>')
def downloadTimedEvals(path = None):
    with pymssql.connect(server, user, password, database) as conn:
        with conn.cursor(as_dict=True) as cursor:
            templateCSV = 'template.csv'
            tempCSV = NamedTemporaryFile(delete=False)
            with open(templateCSV, 'w') as tempCSV:
                #cursor.execute('SELECT * FROM Players INNER JOIN TimedEvaluations ON Players.ID=TimedEvaluations.PlayerID AND TimedEvaluations.TryoutID = %s;', path)
                #cursor.execute('SELECT a.* FROM SkillEvaluations a INNER JOIN (SELECT CriteriaID, MAX(Date) Date FROM SkillEvaluations GROUP BY CriteriaID) b ON a.CriteriaID = b.CriteriaID AND a.Date = b.Date WHERE a.TryoutID = %s AND a.Evaluator = %s AND a.PlayerID = %s;', (tryout, evaluator, player))
                cursor.execute('SELECT a.* FROM Players a INNER JOIN (SELECT PlayerID, TryoutID, MAX(Date) Date FROM TimedEvaluations GROUP BY PlayerID) b ON a.ID=b.PlayerID AND b.TryoutID = %s;', path)
                row = cursor.fetchone()
                fieldnames = row.keys()
                writer = csv.DictWriter(tempCSV, fieldnames=fieldnames)
                writer.writeheader()
                while row:
                    writer.writerow(row)
                    row = cursor.fetchone()
            return send_file(tempCSV.name, as_attachment=True, attachment_filename='timed_evaluations_%s.csv' % path)
    return('error')


@app.route('/downloadSkillEvals/<path>')
def downloadSkillEvals(path = None):
    with pymssql.connect(server, user, password, database) as conn:
        with conn.cursor(as_dict=True) as cursor:
            templateCSV = 'template.csv'
            tempCSV = NamedTemporaryFile(delete=False)
            with open(templateCSV, 'w') as tempCSV:
                cursor.execute('SELECT * FROM Players INNER JOIN SkillEvaluations ON Players.ID=SkillEvaluations.PlayerID AND SkillEvaluations.TryoutID = %s;', path)
                row = cursor.fetchone()
                fieldnames = row.keys()
                writer = csv.DictWriter(tempCSV, fieldnames=fieldnames)
                writer.writeheader()
                while row:
                    writer.writerow(row)
                    row = cursor.fetchone()
            return send_file(tempCSV.name, as_attachment=True, attachment_filename='skill_evaluations_%s.csv' % path)
    return('error')


# MUST be connected to a network for this to work (even with localhost)
if __name__ == '__main__':
    #app.run(debug=True) # 127.0.0.1
    app.run(host='localhost', debug=True) # this works better without known IP? Use for testing.
    #app.run(host='192.168.0.160',debug=True)
    #app.run(host='192.168.1.74',debug=True)
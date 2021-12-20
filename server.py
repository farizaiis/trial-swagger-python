import connexion

app = connexion.App(__name__)

app.add_api("swagger.yml")

if __name__ == "__main__":
    app.run(debug=True)
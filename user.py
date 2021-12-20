from flask import make_response, abort

data = {
    1: {
        "id" : 1,
        "fullName" : "Fariz Afif",
        "email" : "farizaiis@hotmail.com",
        "age": 25
    },
    2: {
        "id" : 2,
        "fullName" : "Fariz",
        "email" : "fariz@gmail.com",
        "age" : 24
    },
    3: {
        "id" : 3,
        "fullName" : "Aisyah",
        "email" : "aisyah@gmail.com",
        "age" : 23
    },
    4: {

        "fullName" : "Test",
        "email" : "test@gmail.com",
        "age" : 22
    },
    5: {
        "fullName" : "Abc",
        "email" : "abc@gmail.com",
        "age" : 21
    },
}

def get_all():
    return[data[key] for key in sorted(data.keys())]


def get_by_id(id):
    if id in data:
        user = data.get(id)
    else:
        abort(
            404, "Cannot found user with id {id}".format(id=id)
        )
    return user

def post(user):
    id = user.get("id", None)
    fullName = user.get("fullName", None)
    email = user.get("email", None)
    age = user.get("age", None)

    if email not in data and email and id and fullName and age is not None:
        data[id] = {
            "id" : id,
            "fullName" : fullName,
            "email" : email,
            "age" : age
        }
        return data[id], 201
    else:
        abort(
            406,
            "User with email {email} already exist".format(id=id)
        )

def put(id, user):
    if id in data:
        data[id]["fullName"] = user.get("fullName")
        data[id]["email"] = user.get("email")
        data[id]["age"] = user.get("age")

        return data[id]

    else:
        abort(
            404, "Cannot found user with id {id}".format(id=id)
        )

def delete(id):
    if id in data:
        del data[id]
        return make_response(
            "Successfully delete the data", 200
        )
    else:
        abort(
            404, "Cannot found user with id {id}".format(id=id)
        )
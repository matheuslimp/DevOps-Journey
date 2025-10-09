db = db.getSiblingDB('admin');

db.createUser({
  user: "appuser",
  pwd: "apppassword",
  roles: [
    { role: "readWrite", db: "admin" }
  ]
});

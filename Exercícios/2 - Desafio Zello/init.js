db = db.getSiblingDB('admin');

// Exemplo: criar um usuário adicional com permissões em outro banco (opcional)
db.createUser({
  user: "appuser",
  pwd: "apppassword",
  roles: [
    { role: "readWrite", db: "admin" }
  ]
});

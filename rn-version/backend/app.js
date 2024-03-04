const express = require('express');
const crypto = require('crypto');
const app = express();
app.use(express.json());

const users = {};

app.post('/enroll', (req, res) => {
  const { username, password } = req.body;
  if (!username || !password) {
    res.status(400).send('Missing username or password');
    return;
  }
  const seed = crypto.randomBytes(20).toString('hex');
  users[username] = { "password":password, "seed":seed };
  console.log(seed);

  res.send(seed);
});

app.get('/verify/:userid', (req, res) => {
    const { userid } = req.params;
    const { token } = req.query;
    if (!userid || !token) {
      res.status(400).send('Missing userid or token');
      return;
    }
    const user = users[userid];
    if (!user) {
      res.status(404).send('User not found');
      return;
    }
    const seed = user["seed"];
    const time = Math.floor(Date.now() / 30000);
    const hash = crypto.createHash('sha1');
    hash.update(seed + time.toString());
    const expectedToken = hash.digest('hex').slice(0, 6);
    if (token === expectedToken) {
      res.send('OK');
    } else {
      res.send('error');
    }
  });

app.listen(3000, () => {
  console.log('Server listening on port 3000');
});
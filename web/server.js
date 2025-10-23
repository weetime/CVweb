import express from "express";
import { WebSocketServer } from "ws";

const app = express();
const port = 8080;

app.use(express.static("public"));
const server = app.listen(port, () => {
  console.log(`Web server running at http://localhost:${port}`);
});

const wss = new WebSocketServer({ server });
wss.on("connection", (ws) => {
  console.log("Client connected.");

  ws.on("message", (msg) => {
    console.log("Received:", msg.toString());
    wss.clients.forEach((client) => {
      if (client.readyState === ws.OPEN) {
        client.send(msg.toString());
      }
    });
  });
});

import { WqcfClient } from "../sdk/node/src/index.js";

const client = new WqcfClient("http://127.0.0.1:8080");
console.log(await client.health());
console.log(await client.capabilities());

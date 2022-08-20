import { WebSV } from "/api.js";

const sv_url = "http://localhost:6969";
const buff_size = 40_000;

export var websv = new WebSV(sv_url, buff_size);

// EXPORTING SERVER URL
export {sv_url};
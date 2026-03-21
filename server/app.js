// This file is the entry point of our application and allows us to run the server.
//reference: https://nodejs.org/en/learn/http/anatomy-of-an-http-transaction#put-it-all-together

const http = require('http'); //http is the library used
 
const port = 3000;

const server = http.createServer((req, res) => { 

    req.on('error', err => { //prevents errors from crashing the program
        //prints the error message and stack trace to stderr
        console.error(err.stack);
    });

    res.end("Wooooahhh, we have made it to the server!"); //write the response to the client and signals end of response
});

server.listen(port, () => {
    console.log("Server is listening on port " + port);
});
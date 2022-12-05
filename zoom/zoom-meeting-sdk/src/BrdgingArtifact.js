/* globals zoomSdk */
import React, {useState } from "react";
import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";
import Button from "react-bootstrap/Button";

function BridgingArtifact() {
    const [user, setUser] = useState(null);
    const [record, setRecord] = useState(false);
    const [input, setInput] = useState("optional summary point");


    function sendData(data) {
        console.log('Sending data');

        const XHR = new XMLHttpRequest();

        const urlEncodedDataPairs = [];

        // Turn the data object into an array of URL-encoded key/value pairs.
        // for (const [name, value] of Object.entries(data)) {
        //   urlEncodedDataPairs.push(`${encodeURIComponent(name)}=${encodeURIComponent(value)}`);
        // }

        urlEncodedDataPairs.push(`time=1`);

        // Combine the pairs into a single string and replace all %-encoded spaces to
        // the '+' character; matches the behavior of browser form submissions.
        const urlEncodedData = urlEncodedDataPairs.join('&').replace(/%20/g, '+');

        // Define what happens on successful data submission
        XHR.addEventListener('load', (event) => {
            alert('Yeah! Data sent and response loaded.');
        });

        // Define what happens in case of error
        XHR.addEventListener('error', (event) => {
            alert('Oops! Something went wrong.');
        });

        // Set up our request
        XHR.open('POST', 'http://127.0.0.1:5000/zoomStart');

        // Add the required HTTP header for form data POST requests
        XHR.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

        // Finally, send our data.
        XHR.send(urlEncodedData);
    }


    function doRequest() {

        let xhr = new XMLHttpRequest();
        xhr.open("POST", "https://1c0a7c8482dc.ngrok.io/zoomstart");
        xhr.setRequestHeader("Content-Type", "application/json");
        let data = `{
            "Id": 78912,
            "Customer": "Jason Sweet",
            "Quantity": 1,
            "Price": 18.00
        }`;

        xhr.send(data);

    }

    function clickMe() {
        console.log('Sending data');
        doRequest();
        setRecord(!record);
    }

    return (
        <div className="App">
            <h1>Hello, {user ? ` ${user.first_name} ${user.last_name}` : " Bridging Artifact user"}!</h1>
            {/*<p>{`User Context Status: ${userContextStatus}`}</p>*/}
            <Button disabled={record} variant="primary" onClick={clickMe}>
                Start Video Snippet
            </Button>
            <Button disabled={!record} variant="primary" onClick={clickMe}>
                End Video Snippet
            </Button>
            <p/>
            {record && <form>
                <input
                    type="text"
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Add optional summary point"
                />
            </form>}
        </div>
    );
}

export default BridgingArtifact;

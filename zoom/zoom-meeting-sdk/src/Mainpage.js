import React from 'react';

import './App.css';
import { ZoomMtg } from '@zoomus/websdk';
import ZoomMtgEmbedded from "@zoomus/websdk/embedded"


ZoomMtg.setZoomJSLib('https://source.zoom.us/2.9.0/lib', '/av');
ZoomMtg.preLoadWasm();
ZoomMtg.prepareWebSDK();
// loads language files, also passes any error messages to the ui
ZoomMtg.i18n.load('en-US');
ZoomMtg.i18n.reload('en-US');

function Mainpage() {

    // setup your signature endpoint here: https://github.com/zoom/meetingsdk-sample-signature-node.js
    var signatureEndpoint = 'http://localhost:4000'
    // This Sample App has been updated to use SDK App type credentials https://marketplace.zoom.us/docs/guides/build/sdk-app
    var sdkKey = 'kBIWVlJFk1ClCvECMxsS3fUQ10MDHBtqKXX5'
    var meetingNumber = '9097539109'
    var role = 0
    var leaveUrl = 'http://localhost:3000'
    var userName = 'Lin'
    var userEmail = 'lq9@uw.edu'
    var passWord = '389426'
    // pass in the registrant's token if your meeting or webinar requires registration. More info here:
    // Meetings: https://marketplace.zoom.us/docs/sdk/native-sdks/web/client-view/meetings#join-registered
    // Webinars: https://marketplace.zoom.us/docs/sdk/native-sdks/web/client-view/webinars#join-registered
    var registrantToken = ''

    function getSignature(e) {
        e.preventDefault();

        fetch(signatureEndpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                meetingNumber: meetingNumber,
                role: role
            })
        }).then(res => res.json())
            .then(response => {
                startMeeting(response.signature)
            }).catch(error => {
            console.error(error)
        })
    }

    function startMeeting(signature) {
        document.getElementById('zmmtg-root').style.display = 'inline'

        ZoomMtg.init({
            leaveUrl: leaveUrl,
            // customize: {
            //     video: {
            //         isResizable: true,
            //         viewSizes: {
            //             default: {
            //                 width: 100,
            //                 height: 60
            //             },
            //             ribbon: {
            //                 width: 30,
            //                 height: 70
            //             }
            //         }
            //     }
            // },
            success: (success) => {
                console.log(success)

                ZoomMtg.join({
                    signature: signature,
                    meetingNumber: meetingNumber,
                    userName: userName,
                    sdkKey: sdkKey,
                    userEmail: userEmail,
                    passWord: passWord,
                    tk: registrantToken,
                    success: (success) => {
                        console.log(success)
                    },
                    error: (error) => {
                        console.log(error)
                    }
                })

            },
            error: (error) => {
                console.log(error)
            }
        })
    }

    return (
        <div className="App">
            <main>
                <h1>Zoom Meeting SDK Sample React</h1>
                <button onClick={getSignature}>Join Meeting</button>
            </main>
        </div>
    );
}
export default Mainpage;

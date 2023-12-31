import React, { useState, useRef, useEffect } from 'react';
import { useSpring, animated } from 'react-spring';
import { Bar } from 'react-chartjs-2';  // <-- Import the Bar component
import 'chart.js/auto'; // This is an important import for chart.js v3 which automatically registers controllers, scales, elements, and plugins.

const Product = () => {
    const [audioFile, setAudioFile] = useState(null);
    const [isRecording, setIsRecording] = useState(false);
    const [mediaRecorder, setMediaRecorder] = useState(null);
    const [chunks, setChunks] = useState([]);
    let audioChunks = [];
    const mediaRecorderRef=useRef(null)
    const [graphData, setGraphData] = useState(null);
    const [graphData2, setGraphData2] = useState(null);
    const chartRef = useRef(null);
    const [gptResponse, setGptResponse] = useState(null);  // <- Add state to store the gpt_response
    const [analysisType, setAnalysisType] = useState('emotion'); // default to 'emotion'


    
    const fadeIn = useSpring({
        opacity: 1,
        from: { opacity: 0 }
    });



    const sendAudioToServer = (audioBlob) => {
        console.log("audioblob: ", audioBlob)
        const blobUrl = URL.createObjectURL(audioBlob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = blobUrl;
        a.download = 'test.ogg';
        document.body.appendChild(a);
        a.click();
        const formData = new FormData();
        formData.append('audio', audioBlob, 'audioRecording.ogg');
        formData.append('analysisType', analysisType);
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            console.log("type of data: ", typeof(data));
            const parsedData = typeof data === 'string' ? JSON.parse(data) : data;
            let labels = parsedData.emotions.map(item => item.emotion);
            let values = parsedData.emotions.map(item => item.score);
            setGraphData({
                labels: labels,
                datasets: [{
                    label: 'Emotions',
                    data: values,
                    backgroundColor: ['#FF6633', '#FFB399', '#FF33FF', '#FFFF99', '#00B3E6', 
                                      '#E6B333', '#3366E6', '#999966', '#99E6E6', '#669900'],
                }],
                options: {
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100
                        }
                    }
                }
            });
            setGptResponse(parsedData.gpt_response)
            if(analysisType==="emotion"){
                let labels = parsedData.IBM.map(item => item.emotion);
                let values = parsedData.IBM.map(item => item.score);
                setGraphData2({
                    labels: labels,
                    datasets: [{
                        label: 'Emotions',
                        data: values,
                        backgroundColor: ['#FF6633', '#FFB399', '#FF33FF', '#FFFF99', '#00B3E6', 
                                          '#E6B333', '#3366E6', '#999966', '#99E6E6', '#669900'],
                    }],
                    options: {
                        scales: {
                            y: {
                                beginAtZero: true,
                                max: 100
                            }
                        }
                    }
                })
            }
        })
        .catch(error => {
            console.error("There was an error sending the audio file", error);
        });
    };


    const handleFileUpload = (event) => {
        const file = event.target.files[0];
        if (file && file.type.startsWith('audio/')) {
            setAudioFile(file);
            
            // Extract the original name and use it when appending to formData
            const formData = new FormData();
            formData.append('audio', file, file.name);
            formData.append('analysisType', analysisType);
            fetch('/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                
                const parsedData = typeof data === 'string' ? JSON.parse(data) : data;
                console.log("type of data: ", typeof(data));
                const labels = parsedData.emotions.map(item => item.emotion);
                const values = parsedData.emotions.map(item => item.score);
                setGraphData({
                    labels: labels,
                    datasets: [{
                        label: analysisType,
                        data: values,
                        backgroundColor: ['#FF6633', '#FFB399', '#FF33FF', '#FFFF99', '#00B3E6', 
                                          '#E6B333', '#3366E6', '#999966', '#99E6E6', '#669900'],
                    }],
                    options: {
                        scales: {
                            y: {
                                beginAtZero: true,
                                max: 100
                            }
                        }
                    }
                
                });
                setGptResponse(parsedData.gpt_response)
                if(analysisType==="emotion"){
                    let labels = parsedData.IBM.map(item => item.emotion);
                    let values = parsedData.IBM.map(item => item.score);
                    setGraphData2({
                        labels: labels,
                        datasets: [{
                            label: 'Emotions',
                            data: values,
                            backgroundColor: ['#FF6633', '#FFB399', '#FF33FF', '#FFFF99', '#00B3E6', 
                                              '#E6B333', '#3366E6', '#999966', '#99E6E6', '#669900'],
                        }],
                        options: {
                            scales: {
                                y: {
                                    beginAtZero: true,
                                    max: 100
                                }
                            }
                        }
                    })
                }
            })
            .catch(error => {
                console.error("There was an error sending the audio file", error);
            });
        }
    };


    const startRecording = () => {
        navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
            const recorder = new MediaRecorder(stream);
            
            recorder.ondataavailable = e => {
                console.log("Data available:", e.data);
                audioChunks.push(e.data);
            };

            recorder.onstop = () => {
                console.log("On stop triggered");
                const blob = new Blob(audioChunks, { 'type' : 'audio/ogg; codecs=opus' });
                sendAudioToServer(blob);
                setAudioFile(blob);
                setIsRecording(false);
                audioChunks = [];

                // Use the useRef to access the stream and cleanup
                const tracks = mediaRecorderRef.current.stream.getTracks();
                tracks.forEach(track => track.stop());
            };

            recorder.start();

            mediaRecorderRef.current = recorder;  // <-- Set the ref to the recorder
            setIsRecording(true);
        });
    };

    const stopRecording = () => {
        if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
            mediaRecorderRef.current.stop();
            console.log("Stopped recording");
        }
    };

    return (
        <animated.div style={fadeIn} className="product-dashboard">
            <div className="graph-dropdown-container">
            <div className="graph-container">
                {!audioFile && <p>Upload or record an audio file to view the analysis graph.</p>}
                {graphData && (analysisType === "parkinsons" ? 
                    <Bar data={graphData} options={graphData?.options} /> :
                    <Bar data={graphData} />
                )}

            </div>
            {analysisType === "emotion" && graphData2 &&
                <div className="graph-container second-graph">
                    <Bar data={graphData2} />
                </div>
            }

                <div className="analysis-type-dropdown">
                    <label>Select Analysis Type: </label>
                    <select value={analysisType} onChange={(e) => setAnalysisType(e.target.value)}>
                        <option value="emotion">Emotion</option>
                        <option value="parkinsons">Parkinson's</option>
                    </select>
                </div>
            </div>
 

            <div className="audio-actions">
                {!isRecording ? (
                    <>
                        <label className="upload-button">
                            Upload Audio File
                            <input type="file" accept="audio/*" onChange={handleFileUpload} hidden />
                        </label>
                        <button className="record-button" onClick={startRecording}>
                            Start Recording
                        </button>
                    </>
                ) : (
                    <button className="record-button stop" onClick={stopRecording}>
                        Stop Recording
                    </button>
                )}
            </div>

            {gptResponse && 
                    <div className="gpt-response-notes">
                        <h3>Notes</h3>
                        <div className="note-content">
                            {gptResponse.split("\n").map((note, index) => <p key={index}>{note}</p>)}
                        </div>
                    </div>
            }
        </animated.div>
    );
}

export default Product;

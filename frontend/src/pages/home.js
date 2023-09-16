import React, {useState, useEffect} from 'react'

const Home = () => {
    const [data, setData] = useState([{}])

    useEffect(()=> {
        fetch("/voiceanalysis").then(
            res => res.json()
        ).then(
            data=> {
                setData(data)
            }
        )
    })

    return(
        <div className="homepage">
            
            <h1 className="headline">BioAcoustix</h1>
            
            {(typeof data.voice==='undefined') ? (
                <p>Loading...</p>
            ):(
                data.voice.map((v, i)=>(
                    <p key={i}>{v}</p>
                ))
            )}
        </div>
    )
}

export default Home
import React, {useState, useEffect} from 'react'

const Product = () => {
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
        <div>
            
            
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

export default Product
import React, { useRef, useState, useEffect } from 'react';
import { useSpring, animated } from 'react-spring';

const Home = () => {
    const [scrollY, setScrollY] = useState(0);
    const segmentRefs = useRef([]);
    const ref = useRef(null);

    const handleScroll = () => {
        setScrollY(window.scrollY);
    };

    useEffect(() => {
        window.addEventListener('scroll', handleScroll, { passive: true });
        return () => {
            window.removeEventListener('scroll', handleScroll);
        };
    }, []);

    const headlineAnimation = useSpring({
        opacity: 1,
        transform: 'translateY(0)',
        from: {
            opacity: 0,
            transform: 'translateY(-50px)'
        }
    });

    const scrollEffect = index => {
        const el = segmentRefs.current[index];
        if (el) {
            const offsetTop = el.offsetTop;
            const difference = scrollY - offsetTop + 500;  // "+ 500" is a tweaking value for smoother animation
            if (difference > 0) {
                return {
                    opacity: 1,
                    transform: `translateY(0)`,
                    transition: `all 0.4s ${index * 0.2}s`  // delay added for sequential animation
                };
            }
        }
        return {
            opacity: 0,
            transform: `translateY(50px)`
        };
    };

    return (
        <div className="homepage" ref={ref}>
            <animated.h1 style={headlineAnimation} className="homepage-headline">BioAcoustix</animated.h1>
            
            <div className="homepage-segment" style={scrollEffect(0)} ref={el => segmentRefs.current[0] = el}>
                <div className="homepage-circle circle-top-left"></div>
                <h2>About the Product</h2>
                <p style={{textAlign: "center"}}>Our product BioAcoustix revolutionizes telehealth data analysis by collecting and analyzing bioacoustic markers from patient speech data. These recordings can be used to identify diseases early and effectively</p>
            </div>
            
            <div className="homepage-segment" style={scrollEffect(1)} ref={el => segmentRefs.current[1] = el}>
                <div className="homepage-circle circle-bottom-right"></div>
                <h2>Why Telehealth is Important</h2>
                <p style={{textAlign: "center"}}>Telehealth is pivotal in modern healthcare, as it provides convenient and accessible medical consultations. Telehealth has grown rapidly since 2020 and will continue to positively impact millions of lives.</p>
            </div>
            
            <div className="homepage-segment" style={scrollEffect(2)} ref={el => segmentRefs.current[2] = el}>
                <div className="homepage-circle circle-top-left"></div>
                <h2>How BioAcoustix Enhances Telehealth Platforms</h2>
                <p style={{textAlign: "center"}}>BioAcoustix acts as a remote diagnosis assistant to clinicians and provides them with a constant stream of speech data through our continuously monitoring dashboards. BioAcoustix uses machine learning algorithms as well as generative AI to provide high-quality and accurate data results.</p>
            </div>

            <div className="homepage-segment" style={scrollEffect(3)} ref={el => segmentRefs.current[3] = el}>
                <div className="homepage-circle circle-bottom-right"></div> {/* Use circle-bottom-right class here */}
                <h2>Check out the voice analytics!</h2>
                <p style={{textAlign: "center"}}><a href="/voice-analytics">Click here!</a></p>
            </div>
        </div>
    )
}

export default Home;

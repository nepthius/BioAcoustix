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
                <p>Our product BioAcoustix revolutionizes...</p>
            </div>
            
            <div className="homepage-segment" style={scrollEffect(1)} ref={el => segmentRefs.current[1] = el}>
                <div className="homepage-circle circle-bottom-right"></div>
                <h2>Why Telehealth is Important</h2>
                <p>Telehealth bridges the gap...</p>
            </div>
            
            <div className="homepage-segment" style={scrollEffect(2)} ref={el => segmentRefs.current[2] = el}>
                <div className="homepage-circle circle-top-left"></div>
                <h2>How BioAcoustix Enhances Telehealth Platforms</h2>
                <p>BioAcoustix, with its advanced tracking...</p>
            </div>
        </div>
    )
}

export default Home;

import Warning from "../assets/mockup1.png"
import AlertWarn from "../assets/mockup2.png"

function Home() {
    return (
        <div className="container alignMiddle">
            <div className="landingContainer alignMiddle">
                <div className="column alignMiddle">
                    <div className="stack">
                        <h2>[Roa]</h2>
                        <h1>Drive smarter,<span style={{fontWeight:"normal"}}><br/>not harder.</span></h1>
                        <button className="button launch" onClick={() => window.location.replace("https://www.roai.tech/record")}>Launch</button>
                    </div>
                </div>
                <div className="right column alignMiddle">
                    <div className="placeholder alignMiddle">
                        <img className="mockup" src={Warning} alt="Phone Mockup"/>
                    </div>
                </div>
            </div>
            <div className="descriptionContainer alignMiddle stack">
                <div className="description" style={{paddingBottom:"50px"}}>
                    <div className="column alignMiddle">
                        <div className="stack">
                            <h1>Let's face it,<span style={{fontWeight:"normal"}}><br/>you're clueless.</span></h1>
                            <h2>But so are we. That's why we built <span style={{fontWeight:"bold"}}>Roa</span>, which uses machine learning to actively keep you alert. <br/><br/>You're welcome.</h2>
                        </div>
                    </div>
                    <div className="right column alignMiddle">
                        <div className="no-shadow placeholder alignMiddle">
                            <h1>[Roa]</h1>
                        </div>
                    </div>
                </div>
                <div className="description alignMiddle">
                    <div className="column alignMiddle">
                        <div className="stack">
                            <h1>Alert and Warn</h1>
                            <h2>Analyzes historical accident data and patterns, traffic density, weather, and more.</h2>
                        </div>
                    </div>
                    <div className="right column alignMiddle">
                        <div className="no-shadow placeholder alignMiddle">
                            <img className="mockup" style={{width:"70%"}} src={AlertWarn} alt="Phone Mockup"/>
                        </div>
                    </div>
                </div>
            </div>
            <div className="landingContainer alignMiddle">
                <div className="column alignMiddle">
                    <div className="stack alignMiddle">
                        <h2 className="centerText">[Roa]</h2>
                        <h1 className="centerText">Drive smarter,<span style={{fontWeight:"normal"}}><br/>not harder.</span></h1>
                        <button className="button launch" onClick={() => window.location.replace("https://www.roai.tech/record")}>Launch Now</button>
                        <h6 className="centerText">Built with ❤️ from Happy Valley</h6>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Home
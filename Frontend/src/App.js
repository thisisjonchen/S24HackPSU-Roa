import './App.css';
import {Route, BrowserRouter as Router, Routes} from "react-router-dom";
import Record from "./pages/record";
import Home from "./pages/home";

function App() {
    return (
        <Router>
            <Routes>
                <Route exact path="/" element={<Home />} />
                <Route path="/record" element={<Record />} />
            </Routes>
        </Router>
    );
}

export default App;

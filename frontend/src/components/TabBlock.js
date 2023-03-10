import { useState } from "react";
import Modules from "./Modules";
import Venues from "./Venues";

const TAB_MODULES = 0;
const TAB_VENUES = 1;

const TabBlock = () => {
    const [block, setBlock] = useState(0);

    const setActive = () => {
        if (block === TAB_MODULES) {
            return (<Modules />)
        }
        else if (block === TAB_VENUES) {
            return (<Venues />);
        }
    }

    return (
        <div>
            <div className="tab-link-container">
                <button
                    className={`tab-link ${(block === TAB_MODULES) ? "tab-link-active" : ""}`}
                    onClick={() => setBlock(TAB_MODULES)}>
                    Modules
                </button>
                <button
                    className={`tab-link ${(block === TAB_VENUES) ? "tab-link-active" : ""}`}
                    onClick={() => setBlock(TAB_VENUES)}>
                    Venues
                </button>
            </div>
            <div className="tab-block">
                {setActive()}
            </div>
        </div>
    );
};

export default TabBlock;
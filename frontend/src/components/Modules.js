import { useEffect, useState } from "react";
import moduleService from "../services/module";
import ModuleItem from "./ModuleItem";

const Modules = () => {
    const [modules, setModules] = useState(null);

    useEffect(() => {
        if (modules == null) {
            moduleService.getAll().then(modules => {
                setModules(modules);
            });
        }
    }, [modules]);

    const getUrl = async (url) => {
        const modules = await moduleService.getUrl(url);
        setModules(modules);
    }

    const searchModule = async (val) => {
        const modules = await moduleService.searchModule(val);
        setModules(modules);
    };

    const modulesList = (modules == null)
        ? []
        : modules["results"].map((module) => {
            return <ModuleItem key={module.id} module={module} />;
        });

    return (
        <>
            <div>
                <input type="search" placeholder="Module Code/Name" onChange={(e) => searchModule(e.target.value)} />
            </div>
            <div className="module-results">
                <ul className="module-list">
                    {modulesList}
                </ul>
            </div>
            <div className="pager module-pager">
                {(modules && modules.previous) ? <input type="button" value="Previous" onClick={() => getUrl(modules.previous)} /> : ""}
                {(modules && modules.next) ? <input type="button" value="Next" onClick={() => getUrl(modules.next)} /> : ""}
            </div>
        </>
    );
}

export default Modules;
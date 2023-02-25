const ModuleItem = ({ module }) => {
    return (
        <div className="module-item">
            <h4>[{module.code}] {module.name}</h4>
            <p>{module.credits} AUs</p>
            <p>{(module.desc.trim() === "") ? <i className="module-nodesc">No module description</i> : module.desc}</p>
        </div>
    );
}

export default ModuleItem;
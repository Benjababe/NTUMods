const ModuleItem = ({ module }) => {
    return (
        <div>
            <h4>[{module.code}] {module.name}</h4>
            <p>{module.credits} CUs</p>
            <p>{module.desc}</p>
        </div>
    );
}

export default ModuleItem;
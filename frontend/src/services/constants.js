const baseUrl = (!process.env.NODE_ENV || process.env.NODE_ENV === 'development')
    ? "http://localhost:8000"
    : "";

const exportObj = {
    baseUrl
};

export default exportObj;
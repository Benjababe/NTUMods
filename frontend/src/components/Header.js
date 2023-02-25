import logoImg from "../assets/images/ntumods-logo.png";

const Header = () => {
    return (
        <div>
            <img
                className="img-logo"
                alt="Logo"
                src={logoImg}></img>
        </div>
    );
}

export default Header;
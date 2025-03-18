import styles from "../styles/Login.module.css";
import logoSalamanca from "../assets/img/logoSalamanca.png";

export function Login() {
    return (
        <div className={styles.bodyl}>
            <div className={styles.logincontainer}>
                <div className={styles.formcontainerl}>
                    <div className={styles.logo}>
                        <img src={logoSalamanca} alt="Salamanca logo"/>
                    </div>
                    <h2 className={styles.title}>Ingresar</h2>
                    <div className={styles.divider}></div>
                    <form>
                        <input type="text" placeholder="Nombre de usuario." className={styles.inputuser}/>
                        <input type="password" placeholder="Contraseña" className={styles.inputpassword}/>
                        <button className={styles.loginbutton}>Ingresar</button>
                    </form>
                    <div className={styles.link}>
                        <a>Aun no estas registrado?</a> 
                        <a href="/Register">Registrate aqui</a>
                    </div>
                    
                </div>
            </div>
        </div>
    )
}
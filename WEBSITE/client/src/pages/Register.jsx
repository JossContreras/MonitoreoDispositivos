import styles from "../styles/Register.module.css";
import logoSalamanca from "../assets/img/logoSalamanca.png";

export function Register() {
    return (
        <div className={styles.bodyr}>
            <div className={styles.container}>
                <div className={styles.formcontainer}>
                    <div className={styles.logo}>
                        <img src={logoSalamanca} alt="Salamanca Logo"/>
                    </div>
                    <h2 className={styles.title}>Registro</h2>
                    <div className={styles.divider}></div>
                    <form>
                        <input type="email" placeholder="Correo Electronico" className={styles.inputemail}/>
                        <input type="text" placeholder="Nombre de Usuario" className={styles.inputusername}/>
                        <div className={styles.passwordcontainer}>
                            <input type="password" placeholder="Contraseña" className={styles.inputpassword}/>
                            <input type="password" placeholder="Confirmar contraseña" className={styles.inputconfirmpassword}/>
                        </div>
                        <button type="submit" className={styles.btn}>Registrarse</button>
                    </form>
                </div>
            </div>
        </div>
    )
}
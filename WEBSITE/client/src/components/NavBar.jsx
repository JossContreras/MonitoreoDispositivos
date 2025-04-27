import styles from "../styles/NavBar.module.css";

export function NavBar() {
    return (
        <div>
            <nav className={styles.NavBar}>
                <h1 className={styles.title}>Inventario</h1>

                <div className={styles.navlinks}>
                    <a href="http://127.0.0.1:8000/monitoreo/home/">Monitoreo</a>
                    <a href="/Inicio">Inicio</a>
                </div>

                <button className={styles.btniniciar}>
                    Usuario
                </button>
            </nav>
        </div>
    )
}
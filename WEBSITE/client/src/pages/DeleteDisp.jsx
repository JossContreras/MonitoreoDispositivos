import { NavBar } from "../components/NavBar";
import styles from "../styles/DeleteDisp.module.css";
import { SearchTool } from "../components/SearchTool";

export function DeleteDisp (){
    return(
        <><NavBar/>
            <div className={styles.containerD}>
                <h1 className={styles.titleD}>Eliminar dispositivo</h1>
                <div className={styles.divider}></div>    
            </div>
            <><SearchTool/></>
            <div className={styles.container}>
                <button className={styles.botoneliminar}>Eliminar</button>
            </div>
        </>
    )
}
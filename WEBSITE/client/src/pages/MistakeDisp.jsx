import { NavBar } from "../components/NavBar";
import { SearchTool } from "../components/SearchTool";
import styles from "../styles/MistakeDisp.module.css";

export function MistakeDisp (){
    return (
        <><NavBar/>
            <div className={styles.containerM}>
                <h1 className={styles.titleM}>Eliminar dispositivo</h1>
                <div className={styles.divider}></div>    
            </div>
            <><SearchTool/></>

            <div className={styles.containerMi}>
                <div className={styles.incidentbox}>
                    <textarea className={styles.incidentdescription} placeholder="Descripcion del incidente"></textarea>
                    <input className={styles.incidentauthor} type="text" placeholder="Realizado por:"/>
                </div>

                <div className={styles.incidentfilters}>
                    <select className={styles.incidentselect}>
                        <option>Fecha de incidente</option>
                    </select>
                    <select className={styles.incidentselect}>
                        <option>Tipo de incidencia</option>
                    </select>
                </div>
                <button className={styles.acceptbutton}>Aceptar</button>
            </div>
        </>
    )
}
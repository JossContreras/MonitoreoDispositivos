import { NavBar } from "../components/NavBar";
import {SearchTool} from "../components/SearchTool";
import styles from "../styles/UpdateDisp.module.css";

export function UpdateDisp (){
    return (
        <><NavBar/>
            <div className={styles.containerU}>
                <h1 className={styles.titleU}>Actualizar Dispositivo</h1>
                <div className={styles.divider}></div>    
            </div>
            <><SearchTool/></>

            <div className={styles.container}>
                <div className={styles.filafiltros}>
                    <select>
                        <option placeholder="Equipo">Equipo</option>
                    </select>
                    <select>
                        <option placeholder="Estado del equipo">Estado del equipo</option>
                    </select>
                    <select>
                        <option placeholder="Fecha de adquisicion">04/03/25</option>
                    </select>
                    <select>
                        <option placeholder="Ubicacion">Ubicacion</option>
                    </select>
                </div>
            
                <div className={styles.filadetalles}>
                    <select>
                        <option placeholder="Marca">Marca</option>
                    </select>
                    <select>
                        <option placeholder="Modelo">Modelo</option>
                    </select>
                        <input type="text" placeholder="Num serie..."/>
                        <input type="text" placeholder="IP"/>   
                </div>
            
                <div className={styles.filadescripcion}>
                    <textarea placeholder="Descripcion de configuracion"></textarea>
                    <textarea placeholder="Parametros personalizados"></textarea>
                    <input type="file" name="icon"/>
                </div>
            
                <button className={styles.botonactualizar}>Actualizar</button>
            </div>
        </>
    )
}
import styles from "../styles/SearchTool.module.css";

export function SearchTool (){
    return (
        <div className={styles.container}>
            <div className={styles.seccionbusqueda}>
                <h2 className={styles.titleA}>Buscar Dispositivo</h2>
                <div className={styles.busquedaform}>
                    <select>
                        <option>Equipo</option>
                    </select>
                    <select>
                        <option>Ubicacion</option>
                    </select>
                    <input type="text" placeholder="No.Serie"/>
                    <button className={styles.botonbuscar}>Buscar</button>
                </div>
            </div>
        
            <hr className={styles.division}/>
        
            <div className={styles.seccionresultado}>
                <h2 className={styles.titleA}>Informacion basica</h2>
                    <div className={styles.infobasica}>
                        <input type="text" value="Switch" readOnly />
                        <input type="text" value="Activo" readOnly />
                        <input type="text" value="20/12/2024" readOnly />
                        <input type="text" value="Edificio principal" readOnly />
                    </div>
        
                    <div className={styles.infodetalles}>
                        <input type="text" value="CISCO" readOnly />
                        <input type="text" value="SF110-24" readOnly />
                        <input type="text" value="JAF1710BBPJ" readOnly />
                        <input type="text" value="192.128.12.01" readOnly/>
                    </div>
            </div>
        </div>
    )
}

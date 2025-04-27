import { useForm } from "react-hook-form";
import { NavBar } from "../components/NavBar";
import styles from "../styles/RegLocation.module.css"
import { createLocate } from "../api/List.api";

export function RegLocation (){

    const {register, handleSubmit, formState: {
        errors
    }, } = useForm()

    const onSubmit = handleSubmit(async (data) => {
       const res = await createLocate(data);
       console.log(res)
    });

    return(
        <><NavBar />
            <div className={styles.containerL}>
                <h1 className={styles.titleL}>Actividad</h1>
                <div className={styles.divider}></div>

                <form className={styles.container} onSubmit={onSubmit}>
                <div className={styles.fila}>
                    <input type="text" placeholder="Ubicacion"
                    {...register("nombre_ubicacion", {required: true})}
                    />{errors.nombre_ubicacion && <span>El dato es requerido</span>}
                    
                    <input type="text" placeholder="Direccion"
                    {...register("direccion", {required: true})}
                    />{errors.direccion && <span>El dato es requerido</span>}
                    
                    <input type="text" placeholder="Ciudad"
                    {...register("ciudad", {required: true})}
                    />
                    
                    <input type="text" placeholder="Pais"
                    {...register("pais", {required: true})}
                    />

                    <button className={styles.botonregistraru}>Registrar</button>
                </div>
                </form>
            </div>
        </>
    )
}
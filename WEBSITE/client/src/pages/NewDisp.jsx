import { useEffect, useState } from "react"
import { createDisp, GetAllUbi, deleteDisp, updateDisp, GetDisp } from "../api/List.api"
import { NavBar } from "../components/NavBar"
import styles from "../styles/NewDisp.module.css"
import {useForm} from "react-hook-form"
import { useParams, useNavigate } from "react-router-dom"

export function NewDisp() {

    //PETICION GET PARA INFORMACION EN SELECTS
    const [list, setList] = useState([]);
    
        useEffect (() => {
            async function loadList () {
                const res = await GetAllUbi()
                setList(res.data);
                //console.log(res);
            }
            loadList();
        }, [])
    ///////////////////////////////////////////////////////////
    
    const {register, handleSubmit, formState: {
        errors
    },setValue } = useForm()

    //PETICION PARA POST Y PUT EN FORMULARIO
    const onSubmit = handleSubmit(async (data1) => {
        if (params.id) {
            await updateDisp(params.id, data1)
        }else {
            const res = await createDisp(data1)
            console.log(res)
        }
        navigate("/List");
    })
    /////////////////////////////////////////////////////////////////

    //PETICION GET PARA MOSTRAR DISP AL ACTUALIZAR
    useEffect (() => {
        async function loadDisp() {
            if (params.id){
                const res = await GetDisp(params.id);
                console.log(res);
                setValue('tipo_elemento', res.data.tipo_elemento)
                setValue('estado', res.data.estado)
                setValue('fecha_adquisicion', res.data.fecha_adquisicion)
                setValue('id_ubicacion', res.data.id_ubicacion)
                setValue('nombre', res.data.nombre)
                setValue('ip', res.data.ip)
            }
        }
        loadDisp();
    }, [])
    ////////////////////////////////////////////////////////////////////////

    //FUNCION PARAMS Y NAVIGATE PARA ELIMINAR ACTUALIZAR REDIRIGIR
    const params = useParams()
    const navigate = useNavigate()
    /////////////////////////////////////////////////////////////////////

    //FORMULARIO
    return ( <><NavBar />
        <div className={styles.containerN}>
            <h1 className={styles.titleN}>Nuevo Dispositivo</h1>
            <div className={styles.divider}></div>
            <form className={styles.container} onSubmit={onSubmit}>
                <div className={styles.filafiltros}>

                    <input type="text" placeholder="Tipo"
                    {...register("tipo_elemento", {required: true})}
                    />{errors.tipo_elemento && <span>El dato es requerido</span>}

                    {/*<input type="text" placeholder="Estado"
                    {...register("estado", {required: true})}
                    />{errors.estado && <span>El dato es requerido</span>}*/}

                    <input type="date" placeholder="Fecha adquisicion"
                    {...register("fecha_adquisicion", {required: true})}
                    />{errors.fecha_adquisicion && <span>El dato es requerido</span>}

                    <select placeholder="Ubicacion"
                    {...register("id_ubicacion", {required: true})}>
                        {list.map(list => (
                            <option key={list.id_ubicacion}>{list.id_ubicacion}</option>
                        ))}
                    </select>{errors.id_ubicacion && <span>El dato es requerido</span>}
                </div>

                <div className={styles.filadetalles}>
                    <input type="text" placeholder="Marca"
                    {...register("nombre", {required: true})}
                    />{errors.nombre && <span>El dato es requerido</span>}

                    <select>
                        <option placeholder="Modelo">Modelo</option>
                    </select>

                    <input type="text" placeholder="Num serie..."/>
                    <input type="text" placeholder="IP"
                    {...register("ip", {required: false})}
                    />{errors.ip && <span>El dato es requerido</span>}
                </div>

                <div className={styles.filadescripcion}>
                    <textarea placeholder="Descripcion de configuracion"></textarea>
                    <textarea placeholder="Parametros personalizados"></textarea>
                    <input type="file" name="icon"/>
                </div>

                <button className={styles.botonactualizar}>Registrar</button>
            </form>
            
            {params.id && <button className={styles.botoneliminar} onClick={async () => {
                const accepted = window.confirm('seguro de eliminar este dispositivo?')
                if (accepted) {
                    await deleteDisp(params.id);
                    navigate("/List");
                }
            }}>Eliminar</button>}
        </div>
    </>    
    )
}
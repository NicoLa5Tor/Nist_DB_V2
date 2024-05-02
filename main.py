from src.objects.insert_data import AddVulns
from flask import Flask,jsonify,request,render_template
from src.objects.update_data import Update 
import threading,asyncio

app = Flask(__name__)
obj_insert  = AddVulns(option=2)
@app.route('/save_data')
def nist():
    start = request.args.get('start_index')
    try: 
        save = obj_insert.insert_data(start_index=start)
        if save:
            return jsonify({
                "response" : "datos almacenados",
                "status" : 200
            })
        else:
            return jsonify({
                "resposne" : "error al guardar datos",
                "status" : 403
            })
    except Exception as e:
        print(f"Error al retornar el valor en la funcion main: {e}")
        return jsonify({
            "data" : None,
            "status" : 500
        })
@app.route('/update_data')
def update_thread():
   global thread_up 
   thread_up = threading.Thread(target=update())
   thread_up.start()
   return jsonify({
       "response" : "Actualizacion en proceso"
   })
def update():
    try:
        
        obj = Update()
        dt = asyncio.run(obj.update_data())
        response = {
            "response" : dt,
            "status": 200
        }
    except Exception as e:
        response = {
            "response":e,
            "status":"error"
        }
    finally:
        return response

    
if __name__ == '__main__':
    app.run(debug=True,port=4000)
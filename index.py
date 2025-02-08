#####################################
## Credits: Giovanni Gaetani Liseo ##
#####################################

from flask import Flask, render_template, jsonify
from pysnmp.hlapi import *
from flaskwebgui import FlaskUI
#from collections import OrderedDict
#import logging

# Configure logging
#log = logging.getLogger('werkzeug')
#log.setLevel(logging.WARNING)


app = Flask(__name__)

# Classe Ponte 
class Ponte:
    def __init__(self, id, link, sorgente, destinazione, indirizzo_ip, nome, tipo, marca, rt):
        self.id = id
        self.link = link
        self.sorgente = sorgente
        self.destinazione = destinazione
        self.indirizzo_ip = indirizzo_ip
        self.nome = nome
        self.tipo = tipo
        self.marca = marca
        self.rt = rt

    @classmethod
    def create_ponti(cls, ponti_data):
        ponti = []
        for data in ponti_data:
            ponte = cls(id=len(ponti) + 1, link=data[0], sorgente=data[1], destinazione=data[2], 
                        indirizzo_ip=data[3], nome=data[4], tipo=data[5], marca=data[6], rt=data[7])
            ponti.append(ponte)
        return ponti
    
    # scan bitrate
    def scan_bitrate(self):
        oid = [...]
        results = {}
        
        for x in range(9):
            oid_name = f"Bitrate {x}"
            full_oid = f"{oid}{x}"
            
            # Invio della richiesta SNMP
            try:
                errorIndication, errorStatus, errorIndex, varBinds = next(
                    getCmd(
                        SnmpEngine(),
                        CommunityData([...], mpModel=0),
                        UdpTransportTarget((self.indirizzo_ip, 161)),
                        ContextData(),
                        ObjectType(ObjectIdentity(full_oid))
                    )
                )
            except Exception as e:
                continue

            if errorIndication or errorStatus:
                continue
            
            valore_snmp = varBinds[0][1].prettyPrint()
            results[oid_name] = round((int(valore_snmp) * 0.001),2)
        
        # Seleziona solo la prima metà dei risultati
        half_length = len(results) // 2
        filtered_results = dict(list(results.items())[half_length:])  # prendo la seconda metà
        return filtered_results
    

    def scan_snmp_apparato(self, marca):
        results = {}
        
        if marca == "ELBER":
            oids = self.oids_elber
            community = [...]
        elif marca == "ERICSSON":
            oids = self.oids_ericsson
            community = [...]
            
        # per ciascuno oid
        for oid_name, oid_info in oids.items():
            oid = oid_info[0]
            moltiplicatore = oid_info[1]
            valore_riferimento = oid_info[2]
            tipo = oid_info[3]
            
            # Determino se l'OID è binario
            is_binario = (tipo == "bin")

            # Invio della richiesta SNMP
            try:
                errorIndication, errorStatus, errorIndex, varBinds = next(
                    getCmd(
                        SnmpEngine(),
                        CommunityData(community, mpModel=0),
                        UdpTransportTarget((self.indirizzo_ip, 161)),
                        ContextData(),
                        ObjectType(ObjectIdentity(oid))
                    )
                )
            except Exception as e:
                results[oid_name] = "Errore"
                continue

            if errorIndication:
                results[oid_name] = "Errore"
                continue
            elif errorStatus:
                results[oid_name] = "Errore"
                continue

            # Ottenimento del valore dall'SNMP
            valore_snmp = varBinds[0][1].prettyPrint()

            # Gestione valori binari
            if is_binario:
                if str(valore_snmp) == str(valore_riferimento):
                    results[oid_name] = "OK"
                else:
                    results[oid_name] = "ALERT"

            # Gestione valori numerici
            elif tipo == "int":
                try:
                    valore_numerico = float(valore_snmp)
                    results[oid_name] = round(valore_numerico * moltiplicatore, 2)
                except ValueError:
                    results[oid_name] = "Errore conversione"

            # Gestione stringhe
            elif tipo == "str":
                results[oid_name] = valore_snmp

        # Aggiungi i risultati del bitrate se siamo in ERICSSON
        if marca == "ERICSSON":
            bitrate_results = self.scan_bitrate()
            #print(bitrate_results)
            results.update(bitrate_results)
        return results    

    
    # community ericsson = [...]
    
    oids_ericsson = { }

    oids_elber = { }


ponti_data = [ ]   

ponti = Ponte.create_ponti(ponti_data)

@app.route('/')
def index():
    ponti_ordinati = sorted(ponti, key=lambda ponte: int(ponte.nome.split()[1])) 
    return render_template('sinottico.html', ponti=ponti_ordinati)


@app.route('/get_snmp_data/<string:marca>/<int:id>', methods=['GET'])
def get_snmp_data(marca,id):
    # Trova il ponte corrispondente
    ponte = next((p for p in ponti if p.id == id), None)

    if not ponte:
        return jsonify({"error": "Ponte non trovato"}), 404
    
    # Esegui la scansione SNMP
    if marca == "ELBER":  # Se marca è "elber"
        snmp_data = ponte.scan_snmp_apparato("ELBER")
    elif marca == "ERICSSON":  # Se marca è "ericsson"
        snmp_data = ponte.scan_snmp_apparato("ERICSSON")
    else:
        snmp_data = {"error": "Marca non supportata"}

    return jsonify(snmp_data)





if __name__ == '__main__':
    ui = FlaskUI(
        app=app,
        width=1024,
        height=768,
        server="flask" 
    )

    try:
        # Prova prima con FlaskWebGUI
        ui.run()
    except Exception as e:
        print(f"Errore con FlaskWebGUI: {e}")
      # Se fallisce, avvia direttamente con Flask sulla porta 8080
    app.run(host='127.0.0.1', port=8080, debug=False)

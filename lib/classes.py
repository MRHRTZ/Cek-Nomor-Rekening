import traceback

from os import system
from sys import platform
from requests import get, post
import json
from terminaltables import AsciiTable

class CheckNorek:
    def __init__(self) -> None:
        self.bankInfo = 'https://cekrekening.id/master/bank?enablePage=0&bankName='
        self.dataBank = {}
        pass

    def clear(self):
        if platform == 'win32':
            system('cls')
        else:
            system('clear')
    def main(self):
        self.clear()
        title = '''
░█▀█░█▀█░█▀▄░█▀▀░█░█░░░█▀▀░█░█░█▀▀░█▀▀░█░█░█▀▀░█▀▄
░█░█░█░█░█▀▄░█▀▀░█▀▄░░░█░░░█▀█░█▀▀░█░░░█▀▄░█▀▀░█▀▄
░▀░▀░▀▀▀░▀░▀░▀▀▀░▀░▀░░░▀▀▀░▀░▀░▀▀▀░▀▀▀░▀░▀░▀▀▀░▀░▀
                    
                  [By MRHRTZ]

Note :
    - Untuk input nomor rekening, input nomor saja, jangan pakai simbol apapun!
    - apabila terdapat bug/pertanyaan bisa kontak author lewat wa : 6285559038021

'''
        menu = '''
1. Lihat ID Bank
2. Check Bank
3. Keluar
'''
        term = '\n[NoRek Checker] > '
        choose = input(title + menu + term)
        while choose != '1' and choose != '2' and choose != '3':
            print('\nPilih angka (1/2/3)!')
            choose = input(term)
        if choose == '1':
            self.clear()
            all = self.printAllBank()
            input(all + '\n\n[Kembali] ')
            self.main()
        elif choose == '2':
            self.inputBank()
        elif choose == '3':
            print('\n\n[ See you later! ]')
            exit(0)

    def inputBank(self):
        id = input('\n[ Masukan ID Bank ] : ')
        rek = input('[ Masukan No Rek ] : ')
        self.clear()
        print()
        out = self.printCheckBank(id, rek)
        input(out + '\n\n[Kembali] ')
        self.main()
    
    def signal_handler(self, sig, frame):
        print('\n\n[ See you later! ]')
        exit(0)

    def getAllBank(self):
        allbank = get(self.bankInfo)
        data = json.loads(allbank.text)
        if data['code'] == '200':
            self.dataBank = data['data']['content']
            return 'ok'
        else:
            return f'Error code : {data["code"]}' 

    def printAllBank(self):
        data_table = [
            ['ID', 'Nama Bank']
        ]
        for info in self.dataBank:
            data_table.append([info['id'], info['bankName']])
        table = AsciiTable(data_table)
        return table.table

    def checkBank(self, bankId, noRek):
        try:
            check = post('https://cekrekening.id/master/cekrekening/report', json={"bankId":bankId,"bankAccountNumber":noRek})
            tojson = json.loads(check.text)
            dataAkun = tojson['data']['laporan']
            if tojson['status'] and dataAkun:
                infoTarget = {
                    'nomor_akun': dataAkun['accountNo'],
                    'nama_bank': dataAkun['bank']['bankName'],
                    'nama_akun_pelaku': dataAkun['accountName'],
                    'info_aduan': dataAkun['kategoriAduan']['keterangan']
                } 
                dataPelapor = tojson['data']['laporanDetail']
                infoPelapor = []
                for lapor in dataPelapor:
                    infoPelapor.append({
                        'jenis_aduan': lapor['tipeAduan']['description'],
                        'nama_pelapor': lapor['reporterFullname'],
                        'nomor_pelapor': lapor['reporterPhoneNumber'],
                        'rugi_sebesar': lapor['totalLoss'],
                        'sumber_media': lapor['sumberMedia']['information'],
                        'waktu_insiden': lapor['incidentDate'],
                        'alamat_pelapor': lapor['reporterAddress'],
                        'nama_dilaporkan': lapor['suspectName'],
                        'nomor_dilaporkan': lapor['suspectPhoneNumber'],
                        'kronologi': lapor['chronology']
                    })
                    return { 'code': 'waspada', 'message': 'Rekening ini dicurigai!', 'target': infoTarget, 'reporter': infoPelapor }
        except:
            input('\n\n[ Terdapat kesalahan, cek inputan dan koneksi anda! ]')
            print(traceback.format_exc())
            self.main()
        else:
            return { 'code': 'aman', 'message': 'NOMER REKENING INI BELUM PERNAH DILAPORKAN TERKAIT TINDAK PENIPUAN APAPUN!\n\nNomor rekening yang belum dilaporkan tidak serta merta mengindikasikan nomor rekening tersebut aman dan terpercaya. Masyarakat dihimbau untuk selalu waspada dalam melakukan transaksi!' }
    
    def printCheckBank(self, bankId, noRek):
        cek = self.checkBank(bankId, noRek)
        if cek['code'] == 'waspada':
            caption = '===========[ Informasi Akun Target ]==========='
            caption += f'''

No Rek : {cek['target']['nomor_akun']}
Bank : {cek['target']['nama_bank']}
Nama : {cek['target']['nama_akun_pelaku']}
Kasus : {cek['target']['info_aduan']}


===========[ Laporan Terverifikasi ]===========
'''
            
            for info in cek['reporter']:
                caption += f'''

Nama dilaporkan : {info['nama_dilaporkan']}
nomor dilaporkan : {info['nomor_dilaporkan']}
Jenis Aduan : {info['jenis_aduan']}
------------------------
Nama Pelapor : {info['nama_pelapor']}
Nomor Pelapor : {info['nomor_pelapor']}
Rugi Sebesar : Rp. {info['rugi_sebesar']}
Sumber Media : {info['sumber_media']}
Waktu Insiden : {info['waktu_insiden']}
Alamat Pelapor : {info['alamat_pelapor']}
Kronologi : {info['kronologi']}

================================================
'''
            return caption
        else: return cek['message']

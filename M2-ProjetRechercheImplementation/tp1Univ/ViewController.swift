//
//  ViewController.swift
//  tp1Univ
//
//  Created by tp on 10/01/2020.
//  Copyright © 2020 tp. All rights reserved.
//

import UIKit

class ViewController: UIViewController {

    @IBOutlet weak var temps: UILabel!
    var timer = Timer();
    var chrono : Int = 0;
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        
        /*let url = URL(string: "http://www.edbali.net")
        let tache = URLSession.shared.dataTask(with: url! {
            (donnee, response, erreur) in
            if let data = donnee{
                let d = String(data: data, encoding: String.Encoding.utf8)
                DispatchQueue.main.async {
                    self.webView.loadHTMLString(d,baseURL:nil)
                }
                print(d)
            }else{
                print("Erreur:"+)
            }
        }*/
    }

    @IBAction func start2(_ sender: Any) {
        timer = Timer.scheduledTimer(timeInterval: 1,target:self,
                                     selector:#selector(self.incrementer),userInfo: nil, repeats: true)
        
    }
    @IBAction func stop2(_ sender: Any) {
        timer.invalidate()
        chrono = 0
        temps.text = "0"    }
    
    @IBAction func pause2(_ sender: Any) {
        timer.invalidate()
        
    }
    @objc func incrementer(){
        chrono += 1;
        temps.text = "\(chrono)"
    }
}


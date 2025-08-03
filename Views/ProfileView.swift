//
//  ProfileView.swift
//  Check-Out!
//
//  Created by ANTS on 8/2/25.
//

import SwiftUI
import SwiftData

struct ProfileView: View {
    @State private var username: String = ""
    var body: some View {
        ZStack(alignment: .top) {
            Color.blue
            VStack(spacing: 0) {                //White banner
                VStack {
                    HStack {
                        Text("Username: ")
                        TextField("Enter your username here...", text: $username)
                            .frame(width: 210)
                        Spacer()
                    }
                    .padding(.leading, 20.0)
                    .padding(.bottom, 5.0)
                    .padding(.top, 65)
                    
                    Circle()
                        .fill(Color.gray)
                        .frame(width: 180, height: 180)
                        .overlay(
                            Image(systemName: "person.fill")
                                .font(.system(size: 50))
                                .foregroundColor(.white)
                            //Change image
                        )
                        .overlay(
                            Circle()
                                .stroke(Color.blue, lineWidth: 10)
                        )
                        .padding(.bottom, -90)
                    
                }
                .frame(maxWidth: .infinity)
                .background(Color.white)
                .clipped()
                .edgesIgnoringSafeArea(.top)
               
                //body
                
                
                Spacer()
                
                
                
            }
        }
        .safeAreaInset(edge: .bottom) {
            Color.clear.frame(height: 25)
        }
    }
}

#Preview {
    ProfileView()
}

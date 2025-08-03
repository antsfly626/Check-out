//
//  ContentView.swift
//  Check-Out!
//
//  Created by ANTS on 8/2/25.
//

import SwiftUI

struct ContentView: View {
    
    @State private var selectedTab = 2
    
    var body: some View {
        TabView(selection: $selectedTab) {
                ProfileView()
                    .tabItem {
                        Image(systemName: "phone.fill")
                }
                .tag(0)
            
            PlaceholderView()
                .tabItem {
                    Image(systemName: "phone.fill")
                }
                .tag(1)
            LibraryView()
                .tabItem {
                    Image(systemName: "phone.fill")
                }
                .tag(2)
            ShelfView()
                .tabItem {
                    Image(systemName: "phone.fill")
                }
                .tag(3)
            FeaturedView()
                .tabItem {
                    Image(systemName: "phone.fill")
                }
                .tag(4)
            
        }
    }
}

#Preview {
    ContentView()
}

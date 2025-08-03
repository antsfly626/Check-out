//
//  ShelfView.swift
//  Check-Out!
//
//  Created by ANTS on 8/2/25.
//

import SwiftUI

struct ShelfView: View {
    var body: some View {
        ZStack {
            Color.orange
            Text("Shelf")
            
        
        }
        .safeAreaInset(edge: .bottom) {
            Color.clear.frame(height: 15)
        }
    }
}

#Preview {
    ShelfView()
}

//
//  FeaturedView.swift
//  Check-Out!
//
//  Created by ANTS on 8/2/25.
//

import SwiftUI

struct FeaturedView: View {
    var body: some View {
        ZStack {
            Color.red
            Text("Featured")
            
        
        }
        .safeAreaInset(edge: .bottom) {
            Color.clear.frame(height: 15)
        }
    }
}

#Preview {
    FeaturedView()
}

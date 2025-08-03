//
//  LibraryView.swift
//  Check-Out!
//
//  Created by ANTS on 8/2/25.
//

import SwiftUI

struct LibraryView: View {
    var body: some View {
        ZStack {
            Color.green
            Text("Library")
        
        }
        .safeAreaInset(edge: .bottom) {
            Color.clear.frame(height: 15)
        }
    }
}

#Preview {
    LibraryView()
}

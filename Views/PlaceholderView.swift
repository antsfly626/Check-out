//
//  PlaceholderView.swift
//  Check-Out!
//
//  Created by ANTS on 8/2/25.
//

import SwiftUI

struct PlaceholderView: View {
    var body: some View {
        ZStack {
            Color.gray
            Text("Coming Soon!")
        }
        .safeAreaInset(edge: .bottom) {
            Color.clear.frame(height: 15)
        }
    }
}

#Preview {
    PlaceholderView()
}

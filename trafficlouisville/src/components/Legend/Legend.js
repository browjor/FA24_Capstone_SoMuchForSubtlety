import React from "react";

const legendItems = [
  { label: "Low Density: <20% of Historical Maximum Detections", color: "green" },
  { label: "Low-Medium Density: 20%-39% of Historical Maximum Detections", color: "lime" },
  { label: "Medium Density: 40%-59% of Historical Maximum Detections", color: "yellow" },
  { label: "Mediium-High Density: 60%-79% of Historical Maximum Detections", color: "orange" },
  { label: "High Density: >80% of Historical Maximum Detections", color: "red" },
];

export default function Legend({ style, className }) {
  const defaultStyle = {
    padding: "10px",
    backgroundColor: "white",
    boxShadow: "0 0 5px rgba(0,0,0,0.3)",
    borderRadius: "5px",
    fontSize: "14px",
    color: "#333",
    lineHeight: "18px",
  };

  const defaultItemStyle = {
    display: "flex",
    alignItems: "center",
    marginBottom: "5px",
  };

  return (
    <div style={{ ...defaultStyle, ...style }} className={className}>
      <strong>Legend</strong>
      <div style={{ marginTop: "5px" }}>
        {legendItems.map((item) => (
          <div key={item.label} style={defaultItemStyle}>
            <span
              style={{
                display: "inline-block",
                width: "200px",
                height: "20px",
                backgroundColor: item.color,
                marginRight: "100px",
              }}
            ></span>
            <span>{item.label}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
